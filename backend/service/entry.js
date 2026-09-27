import { readEntries } from "../repository/entry.js";

export async function getEntries(user) {
    const rows = await readEntries(user);
    return rows.sort(byTime);
}

function byTime(a, b){
    return b.date.localeCompare(a.date) || b.time.localeCompare(a.time);
}