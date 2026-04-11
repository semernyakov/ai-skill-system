# Template System with Tailwind CSS

All project templates use Tailwind CSS for consistent styling.

## Usage

### HTML Templates

Use the base template as a starting point:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        p0: '#ef4444',
                        p1: '#f59e0b',
                        p2: '#3b82f6',
                        p3: '#10b981',
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-100 font-sans">
    <!-- Your content here -->
</body>
</html>
```

### Custom CSS Components

Use centralized CSS components from `.ai/skills/styles/main.css`:

```css
.report-container { @apply max-w-7xl mx-auto p-6; }
.report-header { @apply bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-8 rounded-lg mb-8; }
.severity-badge { @apply px-3 py-1 rounded-full text-xs font-bold; }
```

### Severity Colors

- P0 (Critical): `text-red-500`, `bg-red-500`
- P1 (High): `text-amber-500`, `bg-amber-500`
- P2 (Medium): `text-blue-500`, `bg-blue-500`
- P3 (Low): `text-emerald-500`, `bg-emerald-500`

## Tailwind Configuration

The `tailwind.config.js` scans all template directories:
- `.ai/skills/**/*.html`
- `.cursor/skills/**/*.html`
- `.windsurf/skills/**/*.html`
- `src/**/*.html`
- `templates/**/*.html`

## Adding New Templates

1. Create HTML file in appropriate directory
2. Include Tailwind CDN script
3. Use Tailwind utility classes
4. Reference centralized CSS components if needed
5. Sync with IDEs: `bash .ai/scripts/sync-all.sh`
