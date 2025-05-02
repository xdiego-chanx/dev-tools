import { Argument } from "./Argument";

export class Positional extends Argument {
    public position: number;

    constructor(name: string, position: number) {
        super(name);
        this.position = position;
    }
}
