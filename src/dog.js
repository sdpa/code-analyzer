import { Animal } from "./animal.js";
export class Dog extends Animal {
    constructor(name, breed) {
        super(name);
        this.breed = breed;
    }
    speak() {
        console.log(`${this.name} barks.`);
    }

    // Arrow Function within a class
    dogBark = () => {
        console.log("Woof!");
    }
}