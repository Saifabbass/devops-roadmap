import {createProgressHandler} from '../_lib/progress.mjs';
import {createNeonStore} from '../_lib/neon-store.mjs';

export const onRequest = createProgressHandler({createStore: createNeonStore});
