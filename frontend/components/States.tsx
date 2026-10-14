export function Loading({ label = "Loading verified data" }: { label?: string }) { return <div className="state"><span className="loader" />{label}</div>; }
export function ErrorState({ message }: { message: string }) { return <div className="state error"><strong>Could not connect</strong><span>{message}</span></div>; }
