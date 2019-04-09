$('#reassignModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget)
    var task_id = button.data('id')
    var modal = $(this)
    modal.find('#id_id').val(task_id)
 })
