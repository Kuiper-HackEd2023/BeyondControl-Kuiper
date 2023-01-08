'use strict';

const { app, BrowserWindow } = require('electron');
const nodePath = require('path');
const nodeChildProcess = require('child_process');
const electronIpcMain = require('electron').ipcMain;
var children = [];

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
	if (process.platform !== 'darwin') cleanExit();
});

electronIpcMain.on('runScript', () => {
	if (children.length > 0) {
		console.log('Script running, killing processs');
		children.pop().kill();
	} else {
		// Windows
		let script = nodeChildProcess.spawn('python', ['py/main.py']);
		children.push(script);

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
	}
});

var cleanExit = function () {
	children.forEach((child) => child.kill());
	app.quit();
};

process.on('SIGINT', cleanExit); // catch ctrl-c
process.on('SIGTERM', cleanExit); // catch kill
