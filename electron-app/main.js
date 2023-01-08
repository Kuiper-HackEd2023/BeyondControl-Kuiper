'use strict';

const { app, BrowserWindow } = require('electron');
const nodePath = require('path');
const nodeChildProcess = require('child_process');
const { PythonShell } = require('python-shell');
const electronIpcMain = require('electron').ipcMain;

const createWindow = () => {
	const win = new BrowserWindow({
		width: 800,
		height: 600,
		webPreferences: {
			nodeIntegration: false,
			contextIsolation: true,
			preload: nodePath.join(__dirname, 'preload.js'),
		},
	});

	win.loadFile('index.html');
};

app.whenReady().then(() => {
	createWindow();

	app.on('activate', () => {
		if (BrowserWindow.getAllWindows().length === 0) {
			createWindow();
		}
	});
});

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit();
	}
});

electronIpcMain.on('runScript', () => {
	// Windows
	let script = nodeChildProcess.spawn('cmd.exe', [
		'/c',
		'test.bat',
		'arg1',
		'arg2',
	]);

	console.log('PID: ' + script.pid);

	script.stdout.on('data', (data) => {
		console.log('stdout: ' + data);
	});

	script.stderr.on('data', (err) => {
		console.log('stderr: ' + err);
	});

	script.on('exit', (code) => {
		console.log('Exit Code: ' + code);
	});
});
