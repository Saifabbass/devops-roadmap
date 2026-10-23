import {build} from 'esbuild';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname, join} from 'node:path';
import {createHash} from 'node:crypto';
import {gzipSync} from 'node:zlib';

const deployDir = dirname(fileURLToPath(import.meta.url));
const outputDir = join(deployDir, 'worker-build');
const outputFile = join(outputDir, '_worker.js');
const result = await build({
  entryPoints: [join(deployDir, 'worker-entry.js')],
  outfile: outputFile,
  bundle: true,
  format: 'esm',
  platform: 'browser',
  conditions: ['workerd', 'browser'],
  target: 'es2022',
  minify: true,
  legalComments: 'inline',
  sourcemap: false,
  metafile: true,
  write: false,
  logLevel: 'warning'
});
const external = Object.values(result.metafile.outputs).flatMap(output => output.imports).filter(item => item.external);
if (external.length) throw new Error(`The dashboard worker must be self-contained: ${external.map(item => item.path).join(', ')}`);
if (result.outputFiles.length !== 1) throw new Error('Expected exactly one bundled worker file');
const bundle = result.outputFiles[0].contents;
const gzipBytes = gzipSync(bundle).byteLength;
if (gzipBytes > 3 * 1024 * 1024) throw new Error('The worker exceeds the Workers Free compressed size allowance');
const routes = await readFile(join(deployDir, 'progress-routes.json'), 'utf8');
await mkdir(outputDir, {recursive: true});
await writeFile(outputFile, bundle);
await writeFile(join(outputDir, '_routes.json'), routes);
const report = {
  output: 'deploy/worker-build/_worker.js', bytes: bundle.byteLength, gzipBytes,
  sha256: createHash('sha256').update(bundle).digest('hex'),
  externalImports: external.length, format: 'esm',
  routes: JSON.parse(routes),
  credentials: 'Runtime environment only; no environment files read during build.'
};
await writeFile(join(deployDir, 'worker-build-report.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report));
