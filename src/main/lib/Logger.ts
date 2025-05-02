export class Logger {
    private readonly reset: string = "\x1b[0m";
    private readonly white: string = "\x1b[97m";
    private readonly gray: string = "\x1b[90m";
    private readonly cyan: string = "\x1b[96m";
    private readonly yellow: string = "\x1b[93m";
    private readonly red: string = "\x1b[31m";

    private static readonly _instance = new Logger();

    private constructor() { }

    public static get instance() {
        return Logger._instance;
    }

    public error(message?: any, ...optionalParams: any[]) {
        console.error(`${this.red}${message}${this.reset}`, ...optionalParams);
    }

    public warn(message?: any, ...optionalParams: any[]) {
        console.warn(`${this.yellow}${message}${this.reset}`, ...optionalParams);
    }

    public info(message?: any, ...optionalParams: any[]) {
        console.info(`${this.cyan}${message}${this.reset}`, ...optionalParams);
    }

    public debug(message?: any, ...optionalParams: any[]) {
        console.debug(`${this.gray}${message}${this.reset}`, ...optionalParams);
    }

    public log(message?: any, ...optionalParams: any[]) {
        console.log(`${this.white}${message}${this.reset}`, ...optionalParams);
    }
}