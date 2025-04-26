import { Entity, PrimaryGeneratedColumn } from "typeorm";

@Entity("server")
export class Server {
    @PrimaryGeneratedColumn("uuid")
    id!: string;
}