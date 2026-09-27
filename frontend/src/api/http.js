const BASE = '/api'

export async function request(path, {params, ...options} = {}) {
    let url = BASE + path;
    if (params) {
        const filled = Object.entries(params).filter((item) => item[1] != null);
        const query = new URLSearchParams(filled).toString();
        if (query) {
            url += (url.includes('?')?'&':'?') + query;
        }
    }
    
    const res = await fetch(url, options);
    if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`)
    }   
    return res.json()
}

