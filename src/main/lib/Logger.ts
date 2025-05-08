export class Logger {
    private readonly reset: string = "\x1b[0m";
    private readonly white: string = "\x1b[97m";
    private readonly gray: string = "\x1b[90m";
    private readonly cyan: string = "\x1b[96m";
    private readonly green: string = "\x1b[32m";
    private readonly yellow: string = "\x1b[93m";
    private readonly red: string = "\x1b[31m";

    private static readonly _instance = new Logger();

    private constructor() { }

    public static get instance() {
        return Logger._instance;
    }

    public success(message?: any, ...optionalParams: any[]): void {
        console.log(`${this.green}${message}${this.reset}`, ...optionalParams)
    }

    public error(message?: any, ...optionalParams: any[]): void {
        console.error(`${this.red}${message}${this.reset}`, ...optionalParams);
    }

    public warn(message?: any, ...optionalParams: any[]): void {
        console.warn(`${this.yellow}${message}${this.reset}`, ...optionalParams);
    }

    public info(message?: any, ...optionalParams: any[]): void {
        console.info(`${this.cyan}${message}${this.reset}`, ...optionalParams);
    }

    public debug(message?: any, ...optionalParams: any[]): void {
        console.debug(`${this.gray}${message}${this.reset}`, ...optionalParams);
    }

    public log(message?: any, ...optionalParams: any[]): void {
        console.log(`${this.white}${message}${this.reset}`, ...optionalParams);
    }
}