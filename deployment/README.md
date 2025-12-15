# QuantumAvatar Production Deployment

Dieser Ordner enthält alle nötigen Dateien für das Production Deployment.

## Docker Deployment

```bash
# Lokaler Test mit Docker Compose
docker-compose -f deployment/docker-compose.yml up --build
```

## Heroku Deployment

1. Heroku CLI installieren
2. App erstellen:
   ```bash
   heroku create quantum-avatar-production
   ```

3. API Keys als Environment Variablen setzen:
   ```bash
   heroku config:set PAYPAL_CLIENT_ID=your_client_id
   heroku config:set PAYPAL_CLIENT_SECRET=your_client_secret
   heroku config:set CLAUDE_API_KEY=your_claude_key
   heroku config:set GROK_API_KEY=your_grok_key
   heroku config:set BLACKBOX_API_KEY=your_blackbox_key
   ```

4. Deployen:
   ```bash
   git push heroku main
   ```

## Monitoring

Das System hat integrierte Health-Checks auf `/health` Endpoint.

## Environment Vars

- `FLASK_ENV=production`
- `PAYPAL_CLIENT_ID`
- `PAYPAL_CLIENT_SECRET`
- `CLAUDE_API_KEY`
- `GROK_API_KEY`
- `BLACKBOX_API_KEY`

## HTTPS

Heroku/No-magische automatisch HTTPS für alle Apps.
