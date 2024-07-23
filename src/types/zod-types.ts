import dayjs from 'dayjs';
import zod from 'zod';

export const dayjsSchema = zod.instanceof(
  dayjs as unknown as typeof dayjs.Dayjs,
  {},
);
