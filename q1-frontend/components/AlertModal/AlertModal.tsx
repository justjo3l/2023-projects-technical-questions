import { SetStateAction, Dispatch, FormEvent, useEffect } from "react";
import { TableContents } from "../Table/Table";

interface AlertModalProps {
  useContents: Dispatch<SetStateAction<TableContents>>,
}

export default function AlertModal({useContents}: AlertModalProps) {
  function OnSubmitEvent(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const newAlert = {
      alert: (e.target as any)[0].value,
      status: '',
      updates: []
    }
    useContents((prev) => {
      const newContents = {
        columnTitles: prev.columnTitles,
        rowContents: [...prev.rowContents, newAlert]
      }
      return newContents;
    })
  }
  
  return (
    <form data-testid='form' onSubmit={OnSubmitEvent}>
      <label> Add new alert: </label>
      <input type='text' id='alert' name='alert' />
      <button type='submit'> Add </button>
    </form>
  )
}
