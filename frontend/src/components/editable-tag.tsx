import {Input, Tag, Typography} from 'antd';
import {useState} from 'react';

const tagInputStyle: React.CSSProperties = {
  width: 64,
  height: 22,
  marginInlineEnd: 8,
  verticalAlign: 'top',
};

const tagPlusStyle: React.CSSProperties = {
  height: 22,
  borderStyle: 'dashed',
};

type EditableTagProps = {
  readonly color?: string;
  readonly value: string;
  readonly maxTagLength?: number;
  readonly placeholder?: string;
  readonly onChange: (value: string) => void;
  readonly onBlur?: () => void;
};

export function EditableTag({
  color,
  value,
  maxTagLength,
  placeholder,
  onChange,
  onBlur,
}: EditableTagProps) {
  const [editMode, setEditMode] = useState<boolean>(false);

  const slicedValue = value?.slice(0, maxTagLength || 20);
  return !!editMode ? (
    <Input
      autoFocus
      value={value}
      style={tagInputStyle}
      onChange={({target}) => onChange(target?.value)}
      onBlur={() => {
        onBlur?.();
        setEditMode(false);
      }}
      onPressEnter={() => {
        onBlur?.();
        setEditMode(false);
      }}
    />
  ) : !!value ? (
    <Tag color={color} onClick={() => setEditMode(true)}>
      {`${slicedValue}${slicedValue != value ? '...' : ''}`}
    </Tag>
  ) : (
    <Tag style={tagPlusStyle} onClick={() => setEditMode(true)}>
      {placeholder! || '+ Добавить'}
    </Tag>
  );
}
