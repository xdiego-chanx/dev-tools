import { Argument } from "./argument";

export class Positional extends Argument {
    public position: number;

    constructor(name: string, help: string, position: number) {
        super(name, help);
        this.position = position;
    }
}
