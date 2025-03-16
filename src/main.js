// File: main.js
import { Dog } from "./dog.js";
import { Cat } from "./cat.js";
import { Utility } from "./utility.js";

const dog = new Dog("Buddy", "Golden Retriever");
dog.speak();
dog.dogBark();
dog.animalSound();

const cat = new Cat("Whiskers", "Black");
cat.speak();
cat.asyncMeow();
const catGen = cat.catGeneratorSound();
console.log(catGen.next().value);
console.log(catGen.next().value);

const animal = new Animal("Generic");
const animalGen = animal.generateSound();
console.log(animalGen.next().value);
console.log(animalGen.next().value);

Utility.logMessage("Animal simulation complete.");
Utility.staticArrow();
const staticGen = Utility.staticGenerator();
console.log(staticGen.next().value);
console.log(staticGen.next().value);
Utility.staticFunctionExpression();

function outsideFunction() {
    console.log("Outside Function");
}

outsideFunction();

const outsideFunctionExpression = function() {
    console.log("Outside Function Expression");
}

outsideFunctionExpression();

const outsideArrowFunction = () => {
    console.log("Outside Arrow Function");
}

outsideArrowFunction();

function* outsideGeneratorFunction() {
    yield "Outside generator 1";
    yield "Outside generator 2";
}

const outsideGen = outsideGeneratorFunction();
console.log(outsideGen.next().value);
console.log(outsideGen.next().value);

async function outsideAsyncFunction(){
    console.log("Outside Async Function.");
}
outsideAsyncFunction();

const obj = {
    arrowFunc: () => {
        console.log("Object literal arrow function");
    },
    expressionFunc: function() {
        console.log("Object literal expression function");
    },
    generatorFunc: function* (){
        yield "Object generator 1";
        yield "Object generator 2";
    },
    asyncObjFunc: async function(){
        console.log("Object async function");
    }
};

obj.arrowFunc();
obj.expressionFunc();
const objGen = obj.generatorFunc();
console.log(objGen.next().value);
console.log(objGen.next().value);
obj.asyncObjFunc();

() => {console.log("test")}