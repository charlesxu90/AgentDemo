# Agentic Demo UI

This is the web UI for a general agentic AI demo case.

Adapted from [`DeerFlow`](https://github.com/bytedance/deer-flow).

## Quick Start

### Prerequisites

- [`DeerFlow`](https://github.com/bytedance/deer-flow)
- Node.js (v22.14.0+)
- pnpm (v10.6.2+) as package manager

### Configuration

Set up your own LLM configuration by creating and modifying the .env file.

```bash
cp .env.example .env
```

## Install
```bash
cd web
# Install the dependencies
pnpm install
```

## Run in Development Mode

> [!NOTE]
> Ensure the Python API service is running before starting the web UI.

Start the web UI development server:

```bash
cd web
pnpm dev
```

By default, the web UI will be available at `http://localhost:3000`.

You can set the `NEXT_PUBLIC_API_URL` environment variable if you're using a different host or location.

```ini
# .env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## License

This project is open source and available under the [MIT License](../LICENSE).
