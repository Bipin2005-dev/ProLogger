// Class for storing table elements.
class Data {
  constructor(serial_no, datetime, event_state, event, event_code, event_type) {
    this.serial_no = serial_no;
    this.datetime = datetime;
    this.event_state = event_state;
    this.event = event;
    this.event_code = event_code;
    this.event_type = event_type;
  }
}

let child_list = [];
let curr_list = [];

document.addEventListener("DOMContentLoaded", () => {
  // Parsing the data from the table.
  let data = document.getElementsByTagName("tr");
  let child;
  Array.from(data).forEach((row) => {
    if (row.querySelector(".sl-no")) {
      // Create a Data object corresponding to each row and store it somewhere.
      let serial_no = row.querySelector(".sl-no").innerHTML;
      let datetime = row.querySelector(".date-time").innerHTML;
      let event_state = row.querySelector(".event-state").innerHTML;
      let _event = row.querySelector(".event").innerHTML;
      let event_code = row.querySelector(".event-code").innerHTML;
      let event_type = row.querySelector(".event-type").innerHTML;
      child = new Data(
        serial_no,
        datetime,
        event_state,
        _event,
        event_code,
        event_type
      );
      // Add that element to child_dict, with sl-no as the key, Data as value.
      child_list.push(child);
    }
  });
  curr_list = child_list;

  // Listen for a checked event.
  checkboxes = document.querySelectorAll('thead input[type="radio"]');
  checkboxes.forEach((input) => {
    input.addEventListener("change", (event) => {
      // Allow sorting by only one parameter at a time.
      if (event.target.checked) {
        checkboxes.forEach((input) => {
          if (input != event.target) {
            input.checked = false;
          }
        });

        let sorted_list;

        // Case of Date and Time.
        if (event.target.id === "date_checkbox") {
          // Sort according to Date and Time.
          sorted_list = [...curr_list].sort(
            (a, b) => new Date(a.datetime) - new Date(b.datetime)
          );
        } else if (event.target.id === "es_checkbox") {
          // Sort according to events alphabetically, but also sort by serial_no.
          sorted_list = [...curr_list].sort((a, b) => {
            if (a.event_state === b.event_state) {
              return a.serial_no - b.serial_no;
            } else {
              return a.event_state.localeCompare(b.event_state);
            }
          });
        } else if (event.target.id === "ecode_checkbox") {
          sorted_list = [...curr_list].sort((a, b) => {
            if (a.event_code === b.event_code) {
              return a.serial_no - b.serial_no;
            } else {
              return a.event_code.localeCompare(b.event_code);
            }
          });
        } else if (event.target.id === "sl_checkbox") {
          sorted_list = [...curr_list].sort(
            (a, b) => a.serial_no - b.serial_no
          );
        }

        // Delete all elements of the table and append the new data from sorted list.
        let content = "";
        sorted_list.forEach((element) => {
          console.log("Reached");
          content += `<tr><td class="sl-no">${element.serial_no}</td>
        <td class="date-time">${element.datetime}</td>
        <td class="event-state">${element.event_state}</td>
        <td class="event">${element.event}</td>
        <td class="event-code">${element.event_code}</td>
        <td class="event-type">${element.event_type}</td></tr>`;
        });
        document.getElementsByTagName("tbody")[0].innerHTML = content;
      } else {
        // Delete all elements of the table and append the new data from original list.
        let content = "";
        child_list.forEach((element) => {
          console.log("Reached");
          content += `<tr><td class="sl-no">${element.serial_no}</td>
        <td class="date-time">${element.datetime}</td>
        <td class="event-state">${element.event_state}</td>
        <td class="event">${element.event}</td>
        <td class="event-code">${element.event_code}</td>
        <td class="event-type">${element.event_type}</td></tr>`;
        });
        document.getElementsByTagName("tbody")[0].innerHTML = content;
      }
    });
  });

  // Adding the filtering feature.
  document
    .querySelector("#filter_button")
    .addEventListener("click", (event) => {
      // Filtering by Event State.
      let temp_list = []; // For storing the filtered Data objects.
      const notice_checked = document.getElementById("notice").checked;
      const error_checked = document.getElementById("error").checked;
      let all_checked = document.getElementById("es_all").checked;
      if ((notice_checked && error_checked) || all_checked) {
        temp_list = [...child_list];
      } else if (notice_checked) {
        temp_list = child_list.filter(
          (child) => child.event_state === "notice"
        );
      } else {
        temp_list = child_list.filter((child) => child.event_state === "error");
      }

      // Filtering by event code.
      all_checked = document.getElementById("ecode_all").checked;
      if (!all_checked) {
        for (code of ["E1", "E2", "E3", "E4", "E5", "E6"]) {
          if (!document.getElementById(code).checked) {
            temp_list = temp_list.filter((child) => child.event_code !== code);
          }
        }
      }

      // Changing the table.
      let content = "";
      temp_list.forEach((element) => {
        console.log("Reached");
        content += `<tr><td class="sl-no">${element.serial_no}</td>
        <td class="date-time">${element.datetime}</td>
        <td class="event-state">${element.event_state}</td>
        <td class="event">${element.event}</td>
        <td class="event-code">${element.event_code}</td>
        <td class="event-type">${element.event_type}</td></tr>`;
      });
      document.getElementsByTagName("tbody")[0].innerHTML = content;
      curr_list = temp_list;

      // Uncheck all sort buttons.
      document.querySelectorAll('thead input[type="radio"]').forEach((inp) => {
        inp.checked = false;
      });
    });
});
