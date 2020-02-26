import { useCallback, useState } from 'react';
import { observer } from 'mobx-react';
import { useHistory } from 'react-router-dom';
import { useToggle } from 'react-use';
import Modal from 'react-modal';
import { useStore } from '../../../stores';
import { formatCurrency } from '../../../lib/currency-helpers';

import deleteRound from '@cfpb/cfpb-icons/src/icons/delete-round.svg';

function Details() {
  const { uiStore, eventStore } = useStore();
  const history = useHistory();
  const [selectedID, setSelectedID] = useState(null);
  const [modalOpen, toggleModal] = useToggle(false);

  const confirmDelete = useCallback((eventID) => (evt) => {
    evt.preventDefault();
    evt.stopPropagation();
    setSelectedID(eventID);
    toggleModal(true);
  }, []);

  const eventDeleteHandler = useCallback((andRecurrences = false) => async (evt) => {
    evt.preventDefault();
    await eventStore.deleteEvent(selectedID, andRecurrences);
    toggleModal(false);
  }, [selectedID]);

  const editEvent = useCallback((id) => (evt) => {
    evt.preventDefault();
    history.push(`/calendar/add/${id}/edit`);
  }, []);

  const title = uiStore.selectedDate ? uiStore.selectedDate.toFormat('DDD') : uiStore.currentMonth.toFormat('MMMM, y');
  const events = uiStore.selectedDate
    ? eventStore.eventsByDate.get(uiStore.selectedDate.startOf('day').valueOf())
    : eventStore.eventsByMonth.get(uiStore.currentMonth.startOf('month').valueOf());
  const balance = uiStore.selectedDate
    ? eventStore.getBalanceForDate(uiStore.selectedDate)
    : eventStore.getBalanceForDate(uiStore.currentMonth.endOf('month'));

  return (
    <div className="calendar-details">
      <h2>Transactions for {title}</h2>

      <ul className="calendar-details__events">
        {events &&
          events.map((e) => (
            <li className="calendar-details__event" key={e.id} role="button" onClick={editEvent(e.id)}>
              <div className="calendar-details__event-date">{e.dateTime.toFormat('D')}</div>
              <div className="calendar-details__event-name">{e.name}</div>
              <div className="calendar-details__event-total">{formatCurrency(e.total)}</div>
              <button className="calendar-details__event-delete" onClick={confirmDelete(e.id)}>
                <span dangerouslySetInnerHTML={{__html: deleteRound}} />
              </button>
            </li>
          ))}
      </ul>

      <div className="calendar-details__total">
        <strong className="calendar-details__total-label">Total Balance:</strong>
        <span className="calendar-details__total-value">{formatCurrency(balance || 0)}</span>
      </div>

      <Modal
        className="delete-dialog"
        contentLabel="Event deletion options"
        isOpen={modalOpen}
        onRequestClose={toggleModal}
      >
        <p className="delete-dialog__prompt">Delete Event?</p>
        <ul className="delete-dialog__actions">
          <li className="delete-dialog__action">
            <button
              className="delete-dialog__action-button"
              onClick={eventDeleteHandler(false)}
            >
              Just this event
            </button>
          </li>
          <li className="delete-dialog__action">
            <button
              className="delete-dialog__action-button"
              onClick={eventDeleteHandler(true)}
            >
              This event and all recurrences
            </button>
          </li>
          <li className="delete-dialog__action">
            <button
              className="delete-dialog__action-button"
              onClick={() => toggleModal(false)}
            >
              Cancel
            </button>
          </li>
        </ul>
      </Modal>
    </div>
  );
}

export default observer(Details);
