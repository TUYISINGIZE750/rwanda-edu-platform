#!/usr/bin/env node

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

console.log('🔄 Auto-updating to latest versions...');

try {
  // Read current package.json
  const packagePath = path.join(__dirname, 'package.json');
  const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
  
  console.log('📦 Current version:', packageJson.version);
  
  // Update all dependencies to latest
  console.log('⬆️  Updating dependencies...');
  execSync('npm update', { stdio: 'inherit' });
  
  // Fix any security vulnerabilities
  console.log('🔒 Fixing security issues...');
  execSync('npm audit fix', { stdio: 'inherit' });
  
  // Install any missing dependencies
  console.log('📥 Installing dependencies...');
  execSync('npm install', { stdio: 'inherit' });
  
  console.log('✅ Update complete! All dependencies are now at latest versions.');
  console.log('🚀 You can now run: npm run dev');
  
} catch (error) {
  console.error('❌ Update failed:', error.message);
  process.exit(1);
}