const { app, BrowserWindow, shell } = require('electron');
const fs = require('fs');
const http = require('http');
const path = require('path');
const { pathToFileURL } = require('url');

const isDev = process.env.ELECTRON_START_URL !== undefined;
const distDir = path.join(__dirname, '..', 'dist', 'ta');

let staticServer;
let startUrlPromise;

const mimeTypes = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.webp': 'image/webp',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2'
};

/**
 * Lightweight static file server so the app runs over http:// in Electron.
 */
const startStaticServer = () =>
  new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const url = new URL(req.url, 'http://localhost');
      const requestPath = decodeURIComponent(url.pathname);
      const requestedFile = requestPath === '/' ? '/index.html' : requestPath;
      const filePath = path.normalize(path.join(distDir, requestedFile));

      // Prevent path traversal outside distDir
      if (!filePath.startsWith(distDir)) {
        res.writeHead(403);
        res.end('Forbidden');
        return;
      }

      const serveFile = (finalPath) => {
        const ext = path.extname(finalPath).toLowerCase();
        const contentType = mimeTypes[ext] || 'application/octet-stream';
        fs.readFile(finalPath, (err, data) => {
          if (err) {
            res.writeHead(500);
            res.end('Internal Server Error');
            return;
          }
          res.writeHead(200, { 'Content-Type': contentType });
          res.end(data);
        });
      };

      fs.stat(filePath, (err, stats) => {
        if (!err && stats.isFile()) {
          serveFile(filePath);
          return;
        }
        // SPA fallback to index.html
        const indexPath = path.join(distDir, 'index.html');
        serveFile(indexPath);
      });
    });

    // 0 picks a free port; we record it to load the URL.
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ url: `http://127.0.0.1:${port}`, server });
    });

    server.on('error', reject);
  });

/**
 * Loads Angular either from the dev server or the production build.
 */
const getStartUrl = () => {
  if (startUrlPromise) {
    return startUrlPromise;
  }

  if (process.env.ELECTRON_START_URL) {
    startUrlPromise = Promise.resolve(process.env.ELECTRON_START_URL);
    return startUrlPromise;
  }

// Serve the built app over http instead of file:// to match SPA asset expectations.
  startUrlPromise = startStaticServer().then(({ url, server }) => {
    staticServer = server;
    return url;
  });

  return startUrlPromise;
};

const createWindow = async () => {
  const mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 1024,
    minHeight: 640,
    show: false,
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      partition: 'persist:pandapath'
    }
  });

  const startUrl = await getStartUrl();
  mainWindow.loadURL(startUrl);

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    if (isDev) {
      mainWindow.webContents.openDevTools({ mode: 'detach' });
    }
  });

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
};

app.whenReady().then(async () => {
  await createWindow();

  app.on('activate', async () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      await createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (staticServer) {
      staticServer.close();
    }
    app.quit();
  }
});
