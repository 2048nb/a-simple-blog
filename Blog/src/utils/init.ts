import { getCollectPostIdApi } from '@/utils/request';
import { useAuthStore } from '@/store/auth';

const { currentUser } = useAuthStore();

export const getStarList = async () => {
    const res = await getCollectPostIdApi(Number(currentUser?.id));
    if (res.code === 200) {
        localStorage.setItem('star_post_id', JSON.stringify(res.data.star_post_id));
    }
}

export const localStorageClear = () => {
    localStorage.clear();
}