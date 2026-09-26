import { ref } from 'vue';
import { getEntries } from '../api/entries.js';
import { defineStore } from 'pinia';

export const useEntriesStore = defineStore('entries', () => {
    const entries = ref([]);
    const loading = ref(false);
    const error_message = ref(null);
    async function fetchEntries() {
        loading.value = true;
        try {
            const data = await getEntries();
            entries.value = data;
        } catch (error) {
            error_message.value = error.message;
        } finally {
            loading.value = false;
        }
    }
    return { entries, loading, error_message, fetchEntries };
})