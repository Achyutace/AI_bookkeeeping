import fs from 'node:fs';
import path from 'node:path';
import Papa from 'papaparse';

const DATA_DIR = path.join(import.meta.dirname, '../../data');

export function parseCSV(filePath) {
    return Papa.parse(fs.readFileSync(filePath, 'utf8'), { header: true }).data;
}

