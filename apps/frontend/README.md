# Ta (Angular + Electron)

This package hosts the Angular 16 client that powers CAPRI. You can now run it as a traditional browser SPA or bundle it into desktop apps with Electron.

## Prerequisites

- Node.js 18+
- Yarn 1.x (Classic)

## Setup

```bash
yarn install
cp src/environments/environment.template src/environments/environment.ts
# edit backendHost/llamaHost if they differ
```

## Web development server

```bash
yarn start
```

The Angular CLI serves <http://localhost:4200> with hot reload.

## Desktop development (Electron)

```bash
yarn electron:serve
```

This command runs `ng serve` and Electron concurrently. The Electron shell loads the dev server URL so the Angular hot-reload loop continues to work.

## Building

- Web bundle: `yarn build` (outputs to `dist/ta`).
- Desktop installers: `yarn electron:build` (uses the Angular `electron` configuration to emit relative asset paths, then packages platform-specific artifacts into `release/`).

## Testing

```bash
yarn test
```

Runs the Karma suite. Add desktop smoke tests (e.g., Playwright or Spectron) if you introduce native integrations.
