const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('desktopApp', {
  isDesktop: true
});
