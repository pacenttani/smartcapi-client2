# smartcapi-client-next

PWA untuk wawancara survei, terintegrasi dengan backend ML/NLP & dashboard, dibangun dengan Vue 3, TypeScript, Pinia.

## Fitur
- Rekam audio & transkrip real-time (WebSocket)
- Login & manajemen user
- Progress & hasil wawancara
- PWA-ready (offline, installable)

## Struktur Folder
- `src/components/`: Vue components (UI, Interview, Layout)
- `src/composables/`: Custom hooks (useRecorder, useWebSocket, dsb)
- `src/services/`: API & WebSocket wrapper
- `src/store/`: State management (Pinia)
- `src/types/`: TypeScript type definitions
- `src/utils/`: Helper functions
- `tests/`: Unit & integration tests

## Instalasi

```bash
pnpm install
cp .env.example .env
pnpm dev
```

## Build PWA

```bash
pnpm build
```

## Testing

```bash
pnpm test
```

## Konfigurasi Lingkungan

Lihat `.env.example` dan sesuaikan endpoint backend, WebSocket, dll.

## Kontribusi

Baca [CONTRIBUTING.md](./CONTRIBUTING.md).