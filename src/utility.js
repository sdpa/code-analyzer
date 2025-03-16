export class Utility {
    static logMessage(message) {
        console.log(message);
    }
    // Static Arrow Function
    static staticArrow = () => {
        console.log("Static Arrow Function");
    }
    // Static Generator function
    static *staticGenerator() {
        yield "Static generator sound 1";
        yield "Static generator sound 2";
    }
    // Static Function Expression
    static staticFunctionExpression = function(){
        console.log("Static Function Expression");
    }
}