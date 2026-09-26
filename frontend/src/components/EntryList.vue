<script setup>
defineProps({
    rows: Array
})
</script>

<template>
    <el-table :data="rows">
        <el-table-column prop="id" label="ID" />
        <el-table-column prop="date" label="日期" />
    </el-table>

</template>