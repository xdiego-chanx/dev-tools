export class TraverseError extends Error {
    constructor(message?: string) {
        super(message);
        this.name = "TraverseError";
    }
}