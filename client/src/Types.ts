// Аккаунт
export interface User {
    id_user: number,
    username: string
}

// Сотрудник
export interface Employee {
    id_employee: number,
    full_name: string,
    post: string
    name_organization: string
    address: string
}

// Услуга - географический объект
export interface GeographicalObject {
    id: number;
    feature: string;
    type: string;
    size: number;
    describe: string;
    photo: string;
    status: boolean;
}

export interface Transport {
    id: number;
    name: string;
    type: string;
    describe: string;
    photo: string;
}

export interface Location {
    id: number;
    sequence_number: number;
    id_geographical_object: number;
    id_mars_station: number;
}

// Заявка - марсианская станция
export interface MarsStation {
    id: number,
    type_status: string,
    date_create: string,
    date_form: string,
    date_close: string,
    status_task: number,
    status_mission: number,
    employee: Employee,
    moderator: Employee,
    transport: Transport,
    location: Location[],
    geographical_object: GeographicalObject[]
}

// Для статуса заявки
export interface Option {
    id: number,
    name: string
}

