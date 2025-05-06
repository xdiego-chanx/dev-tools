export abstract class Argument {
    public name: string;
    public help: string;

    constructor(name: string, help: string) {
        this.name = name;
        this.help = help;
    }
}