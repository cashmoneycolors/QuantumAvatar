#!/usr/bin/env python3
"""
MAIN WINDOW MODULE
Provides the primary GUI interface for the Cash Money Colors AI System
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from typing import Optional, Dict, Any, Callable

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import log_system_health, get_logger_instance
from utils.helpers import safe_execute, measure_execution_time

class MainWindow:
    """Main application window for the AI system"""

    def __init__(self, root: tk.Tk, db_manager=None, chatbot=None, ai_manager=None, event_service=None):
        # Logger zuerst setzen
        self.logger = get_logger("CashMoneyColors.MainWindow")

        self.root = root
        self.db = db_manager
        self.chatbot = chatbot
        self.ai_manager = ai_manager
        self.event_service = event_service

        # GUI setup
        self.setup_ui()
        self.setup_event_handlers()

        # Status updates
        self.status_update_interval = 5000  # 5 seconds
        self.schedule_status_update()

    def setup_ui(self):
        """Setup the complete user interface"""
        self.root.title("🎯 CASH MONEY COLORS - AI EMPIRE CONTROL CENTER")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')

        # Setup logger
        self.logger = get_logger_instance("CashMoneyColors.MainWindow")

        # Create main style
        style = ttk.Style()
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TLabel', background='#1a1a1a', foreground='white')
        style.configure('TButton', background='#404040', foreground='white')

        # Create main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame, text="🧠 CASH MONEY COLORS AI SYSTEM",
                              font=('Arial', 28, 'bold'), fg='#00ff00', bg='#1a1a1a')
        title_label.pack(pady=(0, 30))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Main Dashboard Tab
        dashboard_frame = self.create_dashboard_tab()
        self.notebook.add(dashboard_frame, text="📊 Dashboard")

        # AI Agents Tab
        if hasattr(self, 'ai_manager') and self.ai_manager:
            agents_frame = self.create_agents_tab()
            self.notebook.add(agents_frame, text="🤖 AI Agents")

        # Knowledge Base Tab
        if hasattr(self, 'db') and self.db:
            knowledge_frame = self.create_knowledge_tab()
            self.notebook.add(knowledge_frame, text="📚 Knowledge Base")

        # Settings Tab
        settings_frame = self.create_settings_tab()
        self.notebook.add(settings_frame, text="⚙️ Settings")

    def create_dashboard_tab(self):
        """Create the main dashboard tab"""
        frame = ttk.Frame()

        # Status overview
        status_frame = ttk.LabelFrame(frame, text="🔍 System Status", padding=15)
        status_frame.pack(fill=tk.X, pady=(0, 20))

        # Status indicators grid
        self.status_labels = {}
        status_items = [
            ("Database", "database_status"),
            ("AI Agents", "agents_status"),
            ("Tasks", "tasks_status"),
            ("Revenue", "revenue_status"),
            ("Knowledge", "knowledge_status")
        ]

        for i, (label, key) in enumerate(status_items):
            row = i // 3
            col = i % 3

            ttk.Label(status_frame, text=f"{label}:").grid(row=row, column=col*2,
                                                          sticky=tk.W, padx=5, pady=2)
            self.status_labels[key] = ttk.Label(status_frame, text="Loading...")
            self.status_labels[key].grid(row=row, column=col*2+1, sticky=tk.W, padx=5, pady=2)

        # Chat interface
        chat_frame = ttk.LabelFrame(frame, text="💬 AI Nexus Chat", padding=15)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=15, wrap=tk.WORD,
                                                     bg='#2a2a2a', fg='white', font=('Arial', 10))
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Input frame
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Query:").pack(side=tk.LEFT, padx=(0, 10))
        self.chat_input = ttk.Entry(input_frame, font=('Arial', 11), width=60)
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Control buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(side=tk.RIGHT)

        send_btn = ttk.Button(button_frame, text="📤 Send", command=self.send_message)
        send_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = ttk.Button(button_frame, text="🗑️ Clear", command=self.clear_chat)
        clear_btn.pack(side=tk.LEFT)

        # Bind Enter key
        self.chat_input.bind('<Return>', lambda e: self.send_message())

        # Quick actions
        actions_frame = ttk.LabelFrame(frame, text="⚡ Quick Actions", padding=15)
        actions_frame.pack(fill=tk.X)

        actions_row = ttk.Frame(actions_frame)
        actions_row.pack(fill=tk.X, pady=5)

        ttk.Button(actions_row, text="🔄 Update Status",
                  command=self.update_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_row, text="📊 System Stats",
                  command=self.show_system_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_row, text="💰 Revenue Report",
                  command=self.show_revenue_report).pack(side=tk.LEFT, padx=5)

        return frame

    def create_agents_tab(self):
        """Create the AI agents management tab"""
        frame = ttk.Frame()

        # Agent list
        agents_frame = ttk.LabelFrame(frame, text="🤖 Active AI Agents", padding=15)
        agents_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Agent treeview
        columns = ('name', 'status', 'tasks', 'uptime')
        self.agents_tree = ttk.Treeview(agents_frame, columns=columns, show='headings', height=10)

        for col in columns:
            self.agents_tree.heading(col, text=col.title())
            self.agents_tree.column(col, width=100)

        self.agents_tree.pack(fill=tk.BOTH, expand=True)

        # Agent controls
        controls_frame = ttk.LabelFrame(frame, text="🎮 Agent Controls", padding=15)
        controls_frame.pack(fill=tk.X)

        controls_row = ttk.Frame(controls_frame)
        controls_row.pack(pady=10)

        ttk.Button(controls_row, text="▶️ Start All", command=self.start_all_agents).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_row, text="⏹️ Stop All", command=self.stop_all_agents).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_row, text="🔄 Refresh", command=self.update_agents_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_row, text="📈 Performance", command=self.show_performance_stats).pack(side=tk.LEFT, padx=5)

        return frame

    def create_knowledge_tab(self):
        """Create the knowledge base management tab"""
        frame = ttk.Frame()

        # Knowledge statistics
        stats_frame = ttk.LabelFrame(frame, text="📊 Knowledge Statistics", padding=15)
        stats_frame.pack(fill=tk.X, pady=(0, 20))

        self.knowledge_stats = {}
        stat_items = ["Total Entries", "Categories", "Recent Additions", "Quality Score"]

        for item in stat_items:
            ttk.Label(stats_frame, text=f"{item}:").pack(anchor=tk.W, pady=2)
            self.knowledge_stats[item.lower().replace(' ', '_')] = ttk.Label(stats_frame, text="0")
            self.knowledge_stats[item.lower().replace(' ', '_')].pack(anchor=tk.W, padx=(20, 0), pady=2)

        # Search functionality
        search_frame = ttk.LabelFrame(frame, text="🔍 Search Knowledge Base", padding=15)
        search_frame.pack(fill=tk.X, pady=(0, 20))

        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_input_frame, text="Query:").pack(side=tk.LEFT, padx=(0, 10))
        self.knowledge_search = ttk.Entry(search_input_frame, width=50)
        self.knowledge_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        ttk.Button(search_input_frame, text="🔍 Search",
                  command=self.search_knowledge).pack(side=tk.RIGHT)

        # Results display
        results_frame = ttk.LabelFrame(frame, text="📋 Search Results", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True)

        self.knowledge_results = scrolledtext.ScrolledText(results_frame, height=15, wrap=tk.WORD,
                                                         bg='#2a2a2a', fg='white', font=('Arial', 9))
        self.knowledge_results.pack(fill=tk.BOTH, expand=True)

        # Knowledge management
        management_frame = ttk.LabelFrame(frame, text="⚙️ Knowledge Management", padding=15)
        management_frame.pack(fill=tk.X)

        mgmt_buttons = ttk.Frame(management_frame)
        mgmt_buttons.pack(pady=10)

        ttk.Button(mgmt_buttons, text="➕ Add Knowledge",
                  command=self.add_knowledge_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(mgmt_buttons, text="📊 Statistics",
                  command=self.update_knowledge_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(mgmt_buttons, text="🧹 Cleanup",
                  command=self.cleanup_knowledge).pack(side=tk.LEFT, padx=5)

        return frame

    def create_settings_tab(self):
        """Create the settings and configuration tab"""
        frame = ttk.Frame()

        # System settings
        system_frame = ttk.LabelFrame(frame, text="🔧 System Settings", padding=15)
        system_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(system_frame, text="Log Level:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.log_level_var = tk.StringVar(value="INFO")
        ttk.Combobox(system_frame, textvariable=self.log_level_var,
                     values=["DEBUG", "INFO", "WARNING", "ERROR"]).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(system_frame, text="Auto-start Agents:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.autostart_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(system_frame, variable=self.autostart_var).grid(row=1, column=1, sticky=tk.W, pady=5)

        # Save settings button
        ttk.Button(system_frame, text="💾 Save Settings", command=self.save_settings).grid(row=2, column=0, columnspan=2, pady=10)

        # Diagnostics
        diag_frame = ttk.LabelFrame(frame, text="🔍 Diagnostics", padding=15)
        diag_frame.pack(fill=tk.X, pady=(0, 20))

        diag_buttons = ttk.Frame(diag_frame)
        diag_buttons.pack(pady=10)

        ttk.Button(diag_buttons, text="🏥 Health Check", command=self.run_health_check).pack(side=tk.LEFT, padx=5)
        ttk.Button(diag_buttons, text="🔧 System Info", command=self.show_system_info).pack(side=tk.LEFT, padx=5)
        ttk.Button(diag_buttons, text="🗃️ Database Check", command=self.check_database).pack(side=tk.LEFT, padx=5)

        # Debug output
        debug_frame = ttk.LabelFrame(frame, text="🐛 Debug Output", padding=15)
        debug_frame.pack(fill=tk.BOTH, expand=True)

        self.debug_output = scrolledtext.ScrolledText(debug_frame, height=10, wrap=tk.WORD,
                                                    bg='#2a2a2a', fg='#00ff00', font=('Courier', 9))
        self.debug_output.pack(fill=tk.BOTH, expand=True)

        return frame

    def setup_event_handlers(self):
        """Setup event handlers for real-time updates"""
        if self.event_service:
            self.event_service.on('ai_status_update', self.handle_ai_status_update)
            self.event_service.on('task_completed', self.handle_task_completed)
            self.event_service.on('new_knowledge', self.handle_new_knowledge)

    def schedule_status_update(self):
        """Schedule periodic status updates"""
        self.update_status()
        if hasattr(self, 'update_status'):
            self.root.after(self.status_update_interval, self.schedule_status_update)

    def update_status(self):
        """Update all status indicators"""
        try:
            if self.db:
                # Database status
                stats = self.db.get_system_stats()
                self.status_labels['database_status'].config(text=f"✓ {stats.get('knowledge_entries', 0)} entries")
                self.status_labels['knowledge_status'].config(text=".2f")

            if self.ai_manager:
                # AI agents status
                agent_status = self.ai_manager.get_agent_status()
                self.status_labels['agents_status'].config(text=f"✓ {agent_status.get('active_agents', 0)}/{agent_status.get('total_agents', 0)} active")

            if self.db:
                # Tasks status
                self.status_labels['tasks_status'].config(text=f"⚡ {stats.get('pending_tasks', 0)} pending")

            # Revenue status (would need actual revenue tracking)
            self.status_labels['revenue_status'].config(text="€0.00")

            # Log health update
            log_system_health("UI", "HEALTHY")

        except Exception as e:
            self.logger.error(f"Status update failed: {e}")
            for label in self.status_labels.values():
                label.config(text="❌ Error")

    def send_message(self):
        """Send message to AI system"""
        message = self.chat_input.get().strip()
        if not message:
            return

        # Add to display
        self.add_chat_message(f"You: {message}")
        self.chat_input.delete(0, tk.END)

        # Process message
        if self.chatbot:
            threading.Thread(target=self._process_message, args=(message,),
                           daemon=True).start()
        else:
            self.add_chat_message("AI: Chatbot not available")

    def _process_message(self, message):
        """Process message in background thread"""
        try:
            response = safe_execute(self.chatbot.process_query, message)
            if response:
                self.add_chat_message(f"AI: {response}")

                # Save conversation
                if self.db:
                    self.db.save_conversation(message, response)

                # Trigger event
                if self.event_service:
                    self.event_service.trigger('chat_response', {
                        'query': message,
                        'response': response
                    })

        except Exception as e:
            self.add_chat_message(f"Error: {str(e)}")
            self.logger.error(f"Message processing failed: {e}")

    def add_chat_message(self, message):
        """Add message to chat display"""
        timestamp = time.strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] {message}\n")
        self.chat_display.see(tk.END)

    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.delete(1.0, tk.END)

    def update_agents_list(self):
        """Update the agents treeview"""
        if not hasattr(self, 'agents_tree') or not self.ai_manager:
            return

        # Clear existing items
        for item in self.agents_tree.get_children():
            self.agents_tree.delete(item)

        # Add current agents
        agents_status = self.ai_manager.get_agent_status()
        for agent in agents_status.get('agents', []):
            self.agents_tree.insert('', tk.END, values=(
                agent['name'],
                agent['status'],
                'N/A',  # tasks processed (would need to track)
                'N/A'   # uptime (would need to track)
            ))

    def start_all_agents(self):
        """Start all AI agents"""
        if self.ai_manager:
            try:
                self.ai_manager.start_all_agents()
                messagebox.showinfo("Success", "All AI agents started successfully")
                self.update_agents_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start agents: {e}")

    def stop_all_agents(self):
        """Stop all AI agents"""
        if self.ai_manager:
            try:
                self.ai_manager.stop_all_agents()
                messagebox.showinfo("Success", "All AI agents stopped successfully")
                self.update_agents_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop agents: {e}")

    def show_performance_stats(self):
        """Show AI performance statistics"""
        if not self.ai_manager:
            messagebox.showerror("Error", "AI Manager not available")
            return

        # This would need actual performance tracking implementation
        # For now, show basic agent status
        stats = self.ai_manager.get_agent_status()
        stats_text = "\n".join([
            f"Total Agents: {stats.get('total_agents', 0)}",
            f"Active Agents: {stats.get('active_agents', 0)}",
            f"Agent List: {', '.join([a['name'] for a in stats.get('agents', [])])}"
        ])

        messagebox.showinfo("AI Performance Stats", stats_text)

    def update_knowledge_stats(self):
        """Update knowledge base statistics"""
        if not self.db:
            return

        try:
            stats = self.db.get_stats()
            self.knowledge_stats['total_entries'].config(text=str(stats.get('knowledge_entries', 0)))
            self.knowledge_stats['categories'].config(text=str(stats.get('knowledge_categories', 0)))
            self.knowledge_stats['recent_additions'].config(text="N/A")  # Would need to implement
            self.knowledge_stats['quality_score'].config(text="N/A")     # Would need to implement
        except Exception as e:
            self.logger.error(f"Failed to update knowledge stats: {e}")

    def search_knowledge(self):
        """Search the knowledge base"""
        query = self.knowledge_search.get().strip()
        if not query or not self.db:
            return

        try:
            results = self.db.search_knowledge(query, limit=10)
            result_text = f"Search results for: '{query}'\n\n"

            if results:
                for i, result in enumerate(results, 1):
                    result_text += f"{i}. Query: {result.get('query', 'N/A')}\n"
                    result_text += f"   Content: {result.get('content', 'N/A')[:200]}...\n"
                    result_text += f"   Category: {result.get('category', 'general')}\n\n"
            else:
                result_text = "No knowledge found for this query."

            self.knowledge_results.delete(1.0, tk.END)
            self.knowledge_results.insert(tk.END, result_text)

        except Exception as e:
            self.logger.error(f"Knowledge search failed: {e}")
            self.knowledge_results.delete(1.0, tk.END)
            self.knowledge_results.insert(tk.END, f"Search failed: {str(e)}")

    def add_knowledge_dialog(self):
        """Show dialog to add new knowledge"""
        # This would open a dialog window - simplified for now
        messagebox.showinfo("Add Knowledge", "Feature coming soon!")

    def cleanup_knowledge(self):
        """Clean up old knowledge entries"""
        if not self.db:
            return

        try:
            self.db.cleanup_old_entries()
            messagebox.showinfo("Success", "Knowledge base cleanup completed")
            self.update_knowledge_stats()
        except Exception as e:
            messagebox.showerror("Error", f"Cleanup failed: {e}")

    def save_settings(self):
        """Save settings"""
        log_level = self.log_level_var.get()
        autostart = self.autostart_var.get()

        # Save to configuration
        # This would need a config manager
        messagebox.showinfo("Settings", f"Settings saved (implementation needed)\nLog Level: {log_level}\nAuto-start: {autostart}")

    def run_health_check(self):
        """Run system health check"""
        health_issues = []

        # Check database
        if self.db:
            try:
                stats = self.db.get_stats()
                if stats.get('knowledge_entries', 0) == 0:
                    health_issues.append("Warning: Empty knowledge base")
            except Exception as e:
                health_issues.append(f"Database error: {e}")
        else:
            health_issues.append("Database not available")

        # Check AI agents
        if self.ai_manager:
            try:
                agent_status = self.ai_manager.get_agent_status()
                if agent_status.get('active_agents', 0) == 0:
                    health_issues.append("Warning: No active AI agents")
            except Exception as e:
                health_issues.append(f"AI Manager error: {e}")
        else:
            health_issues.append("AI Manager not available")

        # Show results
        if health_issues:
            issue_text = "Health Check Results:\n\n" + "\n".join(f"• {issue}" for issue in health_issues)
        else:
            issue_text = "✅ All systems healthy!"

        self.debug_output.delete(1.0, tk.END)
        self.debug_output.insert(tk.END, issue_text)

    def show_system_info(self):
        """Show system information"""
        import platform
        import sys

        info = f"""
System Information:
• OS: {platform.system()} {platform.release()}
• Python: {sys.version}
• Architecture: {platform.machine()}

Components Status:
• Database: {'✓ Connected' if self.db else '❌ Not Available'}
• AI Manager: {'✓ Active' if self.ai_manager else '❌ Not Available'}
• Chatbot: {'✓ Available' if self.chatbot else '❌ Not Available'}
• Event Service: {'✓ Active' if self.event_service else '❌ Not Available'}
"""

        self.debug_output.delete(1.0, tk.END)
        self.debug_output.insert(tk.END, info)

    def check_database(self):
        """Check database integrity"""
        if not self.db:
            self.debug_output.delete(1.0, tk.END)
            self.debug_output.insert(tk.END, "❌ Database not available")
            return

        try:
            # Run some basic checks
            stats = self.db.get_stats()
            test_query = self.db.search_knowledge("test")  # Should work even with no results

            self.debug_output.delete(1.0, tk.END)
            self.debug_output.insert(tk.END, "✅ Database integrity check passed\n\n")
            self.debug_output.insert(tk.END, f"Statistics: {stats}\n")
            self.debug_output.insert(tk.END, "Query test: Successful")

        except Exception as e:
            self.debug_output.delete(1.0, tk.END)
            self.debug_output.insert(tk.END, f"❌ Database integrity check failed: {e}")

    def show_system_stats(self):
        """Show comprehensive system statistics"""
        if not self.db:
            messagebox.showerror("Error", "Database not available")
            return

        try:
            stats = self.db.get_stats()

            stats_text = ""
            stats_text += f"Knowledge Base: {stats.get('knowledge_entries', 0)} entries\n"
            stats_text += f"Categories: {stats.get('knowledge_categories', 0)}\n"
            stats_text += f"Total Conversations: {stats.get('total_conversations', 0)}\n"
            stats_text += f"Avg Response Time: {stats.get('avg_response_time', 0):.2f}s\n"
            stats_text += f"Tasks: {stats.get('total_tasks', 0)} total ({stats.get('pending_tasks', 0)} pending)\n"
            stats_text += f"Revenue: €{stats.get('total_revenue', 0):.2f} total, €{stats.get('recent_revenue', 0):.2f} this month\n"

            # AI Performance (if available)
            if self.ai_manager:
                agent_stats = self.ai_manager.get_agent_status()
                stats_text += f"\nAI Agents: {agent_stats.get('active_agents', 0)}/{agent_stats.get('total_agents', 0)} active"

            messagebox.showinfo("System Statistics", stats_text)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to get system stats: {e}")

    def show_revenue_report(self):
        """Show revenue report"""
        if not self.db:
            messagebox.showerror("Error", "Revenue tracking not available")
            return

        try:
            revenue_stats = self.db.get_revenue_stats()

            report = ""
            report += ".2f"
            report += ".2f"
            report += ".2f"

            # Revenue by source
            report += "\n\nRevenue by Source:"
            for source, amount in revenue_stats.get('revenue_by_source', {}).items():
                report += ".2f"

            messagebox.showinfo("Revenue Report", report)

        except Exception as e:
            messagebox.showerror("Error", f"Revenue report failed: {e}")

    # Event handlers
    def handle_ai_status_update(self, data):
        """Handle AI status update event"""
        self.update_agents_list()

    def handle_task_completed(self, data):
        """Handle task completed event"""
        self.add_chat_message(f"✅ Task completed: {data.get('type', 'N/A')}")

    def handle_new_knowledge(self, data):
        """Handle new knowledge added event"""
        self.add_chat_message(f"🧠 Knowledge added: {data.get('query', '')[:50]}...")

    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit? All AI agents will be stopped."):
            # Stop all agents gracefully
            if self.ai_manager:
                try:
                    self.ai_manager.stop_all_agents()
                except:
                    pass

            self.root.destroy()

def create_main_window(db_manager=None, chatbot=None, ai_manager=None, event_service=None):
    """Factory function to create main window"""
    root = tk.Tk()
    app = MainWindow(root, db_manager, chatbot, ai_manager, event_service)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    return root, app
