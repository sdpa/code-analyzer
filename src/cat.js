import { Animal } from "./animal.js";
export class Cat extends Animal {
    constructor(name, color) {
        super(name);
        this.color = color;
    }
    speak() {
        console.log(`${this.name} meows.`);
    }

    async asyncMeow() {
        return new Promise(resolve => {
            setTimeout(() => {
                console.log(`${this.name} async meow.`);
                resolve();
            }, 500);
        });
    }

    * catGeneratorSound() {
        yield "Cat sound 1";
        yield "Cat sound 2";
    }
}