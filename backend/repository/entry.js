import path from 'node:path';
import { readdir } from 'node:fs/promises';

import { parseCSV } from '../utils/csv.js';

const ROOT_DIR = path.join(import.meta.dirname, '../../data');
// parseCSV return string, so need be converted to int
const NUMBER_FIELDS = ['id', 'amount', 'status'];

/**
 * 读取某用户所有entries
 * 
 * @param {string} user
 * @returns {Promise<Array<Object>>} entries 
 */
export async function readEntries(user) {
    const filePath = path.join(ROOT_DIR, user, 'entries');
    
    let files;
    try {
        const names = await readdir(filePath);
        files = names.filter(name => name.endsWith('.csv'));
    } catch (err) {
        if (err.code === 'ENOENT') {
            return [];
        }
        throw err;
    }
    
    const rows = (await Promise.all(files.map((name) => {
        return parseCSV(path.join(filePath, name));
    }))).flat().map(normalizeRow);

    return rows
}

function normalizeRow(row) {
    const out = {};
    for (const key in row) {
        out[key] = (NUMBER_FIELDS.includes(key)) ? parseFloat(row[key]) : row[key];
    }
    return out;
}
