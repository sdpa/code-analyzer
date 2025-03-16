export class Animal {
    constructor(name) {
        this.name = name;
    }
    speak() {
        console.log(`${this.name} makes a noise.`);
    }

    animalSound = function() {
        console.log("Generic animal sound");
    };

    *generateSound() {
        yield "Animal sound 1";
        yield "Animal sound 2";
    }
}
