"use client";

import { Controller, type Control, type FieldValues, type Path } from "react-hook-form";

interface FormFieldProps<T extends FieldValues> {
  control: Control<T>;
  name: Path<T>;
  label?: string;
  placeholder?: string;
  type?: string;
}

export default function FormField<T extends FieldValues>({
  control,
  name,
  label,
  placeholder,
  type = "text",
}: FormFieldProps<T>) {
  return (
    <Controller
      control={control}
      name={name}
      render={({ field, fieldState: { error } }) => (
        <div className="space-y-2">
          {label && (
            <label htmlFor={name} className="block text-sm font-medium">
              {label}
            </label>
          )}
          <input
            {...field}
            id={name}
            type={type}
            placeholder={placeholder}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {error && (
            <p className="text-sm text-red-500">{error.message}</p>
          )}
        </div>
      )}
    />
  );
}

