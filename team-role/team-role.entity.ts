import { Entity, PrimaryGeneratedColumn } from "typeorm";

@Entity("team_role")
export class TeamRole {
    @PrimaryGeneratedColumn()
    id!: number;
}