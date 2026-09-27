import { describe, it, expect } from 'vitest'
import { parseCSV } from '../utils/csv.js'
import { readEntries } from '../repository/entry.js'

console.log(readEntries('齐乐辰'))
describe('parseCSV', () => {
    it('should parse csv to array with dict', () => {
        const path1 = '/Users/achyutace/Desktop/记账/backend/test/data/2026_09.csv'
        const result = parseCSV(path1)
        expect(result).toEqual([{
            id: '114514',
            date: '2026-08-06',
            time: '19:19:08',
            category: '测试',
            tag: '测试',
            amount: '114.51',
            account: '测试',
            status: '0'
        }]);
    });
});

describe('readEntries', () => {
    it('just test', async () => {
        expect(await readEntries('齐乐辰')).toEqual([{
            id: 114514,
            date: '2026-08-06',
            time: '19:19:08',
            category: '测试',
            tag: '测试',
            amount: 114.51,
            account: '测试',
            status: 0
        }]);
    });
});
// describe('parseCSV', () => {
//     it('should parse CSV string into an array of objects', () => {
//         const csvString = 'name,age\nAlice,30\nBob,25';
//         const result = parseCSV(csvString);
//         expect(result.data).toEqual([
//             { name: 'Alice', age: '30' },
//             { name: 'Bob', age: '25' }
//         ]);
//     });

//     it('should handle empty CSV string', () => {
//         const csvString = '';
//         const result = parseCSV(csvString);
//         expect(result.data).toEqual([]);
//     });

//     it('should handle CSV string with only headers', () => {
//         const csvString = 'name,age';
//         const result = parseCSV(csvString);
//         expect(result.data).toEqual([]);
//     });
// }); 
