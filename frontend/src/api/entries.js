import { request } from './http.js'

export function getEntries() {
    return request('/entries', {'method': 'GET'})
}

