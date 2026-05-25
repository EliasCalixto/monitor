# Setup del Dashboard de Notion en GitHub Pages

Pasos manuales que **tú** tienes que hacer una sola vez. El código ya está listo en el repo.

URL final del dashboard: **https://eliascalixto.github.io/monitor/**

---

## 1. Crear la integración en Notion

1. Abre <https://www.notion.so/profile/integrations>.
2. Click en **+ New integration**.
3. Nombre: `Monitor Dashboard` (o el que quieras).
4. Associated workspace: el workspace donde vive tu página Monitor.
5. Type: **Internal**.
6. Click **Save**.
7. En la pestaña **Configuration** copia el **Internal Integration Secret** (empieza con `secret_` o `ntn_`). Guárdalo, lo necesitarás en el paso 3.

## 2. Compartir tu página Monitor con la integración

> Sin esto la API te devuelve 404 porque la integración no ve la página.

1. Abre tu página **Monitor** en Notion.
2. Arriba a la derecha click en `···` → **Connections** (o "Conexiones").
3. Busca el nombre de tu integración (`Monitor Dashboard`) y dale acceso.
4. La integración hereda permiso a **todas** las sub-páginas y databases hijas.

### Obtener el Page ID

La URL de tu página se ve así:

```
https://www.notion.so/Monitor-1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d
```

El page ID son los **últimos 32 caracteres hex** (con o sin guiones). En el ejemplo: `1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d`. Cópialo.

## 3. Agregar los secrets en GitHub

1. Ve a <https://github.com/EliasCalixto/monitor/settings/secrets/actions>.
2. Click **New repository secret** y crea estos dos:

   | Name             | Value                                                    |
   | ---------------- | -------------------------------------------------------- |
   | `NOTION_TOKEN`   | El secret de tu integración (paso 1)                     |
   | `NOTION_PAGE_ID` | El page ID de Monitor (paso 2)                           |

## 4. Permitir que el workflow haga push

1. Ve a <https://github.com/EliasCalixto/monitor/settings/actions>.
2. Baja hasta **Workflow permissions**.
3. Selecciona **Read and write permissions**.
4. Guarda.

> Si no haces esto, el workflow corre pero falla al hacer `git push` con error 403.

## 5. Correr el workflow por primera vez

1. Ve a <https://github.com/EliasCalixto/monitor/actions/workflows/sync-notion.yml>.
2. Click **Run workflow** → branch `main` → **Run workflow**.
3. Espera ~30 seg. Cuando termine en verde, debería haber un nuevo commit `chore: sync Notion data ...` en `main` actualizando `docs/data.json`.

A partir de aquí corre automáticamente cada 15 minutos.

## 6. Activar GitHub Pages

1. Ve a <https://github.com/EliasCalixto/monitor/settings/pages>.
2. Source: **Deploy from a branch**.
3. Branch: `main` · Folder: `/docs`.
4. Click **Save**.
5. Espera ~1 minuto y abre <https://eliascalixto.github.io/monitor/>.

---

## Probar local antes de hacer push

```powershell
# Carga tu token a la sesion (NO lo escribas en archivos)
$env:NOTION_TOKEN = "secret_xxx..."
$env:NOTION_PAGE_ID = "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d"

python scripts/fetch_notion.py
```

Esto genera `docs/data.json` localmente. Después sirve `docs/` con cualquier servidor estático:

```powershell
# Python tiene un servidor built-in
python -m http.server -d docs 8000
```

Y abre <http://localhost:8000>.

---

## Troubleshooting

- **`object_not_found` o 404 en el workflow** → no compartiste la página con la integración (paso 2).
- **El dashboard muestra "No se encontraron databases"** → las databases hijas no son inline; muévelas dentro de la página Monitor o ejecuta el script y revisa `docs/data.json` para ver qué encontró.
- **El workflow corre pero no commitea** → no diste write permission (paso 4) o `data.json` no cambió.
- **Las páginas no se actualizan** → GitHub Pages cachea ~10 min. Fuerza recarga con Ctrl+F5.
- **No quieres esperar 15 min entre updates** → edita el cron en `.github/workflows/sync-notion.yml`. El mínimo práctico en GitHub Actions gratis es ~5 min (`*/5 * * * *`).

## Notas de seguridad

- El `data.json` es **público** (cualquiera con la URL del Pages lo puede leer). No publiques databases con info privada.
- Si necesitas privacidad: cambia el repo a privado y usa **GitHub Pages Private** (requiere plan Pro/Team) o migra a Cloudflare Pages con auth.
- Si filtras el token por accidente: regrésate a la página de integraciones de Notion y haz **Regenerate** del secret.
