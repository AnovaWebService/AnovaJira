import {Button, Popover} from "antd";
import { ReactNode } from "react";

type MarkdownPopoverProps = {
  readonly open?: boolean;
  readonly onClose?: () => void;
  readonly onMarkdownChanged?: (selectedText: string) => void;
  readonly children: ReactNode;
};

export function MarkdownPopover({
  open,
  onClose,
  onMarkdownChanged,
  children,
}: MarkdownPopoverProps) {
  return (
    <Popover
      title={null}
      content={
        <Button.Group>
          <Button type="text">B</Button>
          <Button type="text">I</Button>
          <Button type="text">U</Button>
          <Button type="text">S</Button>
        </Button.Group>
      }
    >
      {children}
    </Popover>
  );
}
