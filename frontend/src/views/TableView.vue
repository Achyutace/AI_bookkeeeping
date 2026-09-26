<script setup>
import { onMounted } from 'vue';
import { useEntriesStore } from '../stores/entries';
import EntryList from '../components/EntryList.vue';

const store = useEntriesStore();

onMounted(() => {
    store.fetchEntries();
});
</script>

<template>
    <h2>数据看表</h2>
    <EntryList :rows="store.entries" />
</template>