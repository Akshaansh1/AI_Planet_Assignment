export interface Stack {
    id: number;
    name: string;
    description: string;
    definition?: {
        nodes: any[];
        edges: any[];
    };
}

export interface Message {
    id: number;
    text: string;
    sender: 'user' | 'bot';
}
