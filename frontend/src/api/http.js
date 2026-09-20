const BASE = '/api'

export async function request(path, options = {}) {
    const res = await fetch(BASE + path, options)
    if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`)
    }   
    return res.json()
}