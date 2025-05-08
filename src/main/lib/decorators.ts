import { Logger } from "./logger";

const logger: Logger = Logger.instance;

// function interruptible() {
//     return function(target: any, key: string, descriptor: PropertyDescriptor) {
//       const original = descriptor.value;
//       descriptor.value = function(...args: any[]) {
//         return original.apply(this, args); // ✅ keeps `this`
//       };
//     };
//   }
  

export function interruptible() {
    return function (_: any, __: string, descriptor: PropertyDescriptor) {
        const original = descriptor.value;
        
        descriptor.value = function (...args: any[]) {
            const handleInterrupt = () => {
                logger.error("Operation interrupted by user.");
                process.exit(130);
            };

            process.once("SIGINT", handleInterrupt);

            try {
                return original.apply(this, args);
            } finally {
                process.off("SIGINT", handleInterrupt);
            }


        };

        return descriptor;
    }
}

export function requires(key: string) {
    return function (_: any, property: string, descriptor: PropertyDescriptor) {
        const originalMethod = descriptor.value;

        descriptor.value = function (args: Map<ArgK, ArgV>, ...rest: any[]) {
            if (!(args instanceof Map)) {
                throw new Error(`Method '${property}' requires a Map argument but got: ${args}`);
            }

            if (!args.has(key)) {
                throw new Error(`Missing required argument '${key}' in method '${property}'`);
            }

            return originalMethod.apply(this, [args, ...rest]);
        };

        return descriptor;
    };
}
