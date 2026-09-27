import { ref } from 'vue';
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
    const currentUser = ref(null);
    function setUser(user) {
        currentUser.value = user;
    }
    return { currentUser, setUser };
})