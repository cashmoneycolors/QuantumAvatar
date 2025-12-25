#!/bin/bash

# Setup Production Environment für QuantumAvatar

echo "🚀 QuantumAvatar Production Setup starten..."

# Copy env template
cp ../.env.example ../.env

echo "✅ .env Datei aus .env.example erstellt"

# Instructions
echo ""
echo "📝 Bitte bearbeite die .env Datei und füge deine echten API-Keys ein:"
echo ""
echo "1. PayPal Business Account Keys (kostenlos):"
echo "   - Folg API-Zugang:" echo "     Der Zugang erfolgt über die PayPal Developer Portal"
echo "     -if die Seite nicht verfügbar ist, wurde das Account zu einem regulären PayPal Konto wurde downgradiert"
echo "     -Für Business-Standardeinstellungen im Production-Modus."
echo ""
echo "2. AI Keys (~$30 einmalig):"
echo "   - Claude: https://console.anthropic.com/"
echo "   - Grok: https://console.x.ai/"
echo "   - BlackBox: https://www.blackbox.ai/"
echo ""
echo "3. Nach Eingabe der Keys:"
echo "   python test_production_config.py"

echo ""
echo "🔥 dann ready für live deployment!"
