<script setup>
import { onMounted } from 'vue';
import { useEntriesStore } from '../stores/entries';
import EntryList from '../components/EntryList.vue';
import { useUserStore } from '../stores/user.js';

const entriesStore = useEntriesStore();
const userStore = useUserStore();
userStore.setUser('齐乐辰') //后面改

onMounted(() => {
    entriesStore.fetchEntries(userStore.currentUser);
});
</script>

<template>
    <h2>数据看表</h2>
    <EntryList :rows="entriesStore.entries" />
</template>