import {reactive, readonly} from 'vue'

export class Store{
    state;

    constructor() {
        let data = this.date();
        this.setup(data);
        this.state = reactive(data);

        if (this.constructor == Store) {
            throw new Error("Abstract classes can't be instantiated.");
        }
    }

    data() {
        throw new Error('Method data() must be implemented');
    }

    setup(data){}

    getState(){
        return readonly(this.state);
    }

}