import { request } from './http.js'

export function getEntries(user) {
    return request('/entries', {'params': {'user': user}, 'method': 'GET'})
}

