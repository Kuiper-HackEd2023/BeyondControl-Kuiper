const nodeChildProcess = require('child_process');

module.exports = {
	packagerConfig: {},
	rebuildConfig: {},
	makers: [
		{
			name: '@electron-forge/maker-squirrel',
			config: {},
		},
		{
			name: '@electron-forge/maker-zip',
			platforms: ['darwin'],
		},
		{
			name: '@electron-forge/maker-deb',
			config: {},
		},
		{
			name: '@electron-forge/maker-rpm',
			config: {},
		},
	],
	hooks: {
		generateAssets: async (forgeConfig, platform, arch) => {
			// Windows
			let script = nodeChildProcess.spawn('cmd.exe', ['/c', 'install.bat']);

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
		},
	},
};
